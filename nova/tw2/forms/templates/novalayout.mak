<%namespace name="tw" module="tw2.core.mako_util"/>\
<div ${tw.attrs(attrs=w.attrs)}>
   % for c in w.children_hidden:
    ${c.display() | n}
   % endfor
   % for i,c in enumerate(w.children_non_hidden):
    <div class="content-block ${'part_'+c.part if hasattr(c, 'part') else 'full'}">
		<h1>${c.label} ${"(Required)" if getattr(c, 'required', False) else ""}</h1>
		<div class="content">
			<p>
				${c.display() | n}
				<span id="${c.compound_id or ''}:error" class="error">${c.error_msg or ''}</span>
			</p>
		</div>
	</div>
   % endfor
</div>
